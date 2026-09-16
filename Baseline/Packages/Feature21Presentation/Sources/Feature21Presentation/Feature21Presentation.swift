import Feature21Domain
import Feature21Data

public enum Feature21PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature21DomainModel = Feature21DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
