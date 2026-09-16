import Feature33Domain
import Feature33Data

public enum Feature33PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature33DomainModel = Feature33DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
