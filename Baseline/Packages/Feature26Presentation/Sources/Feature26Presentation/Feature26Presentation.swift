import Feature26Domain
import Feature26Data

public enum Feature26PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature26DomainModel = Feature26DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
