import Feature23Domain
import Feature23Data

public enum Feature23PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature23DomainModel = Feature23DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
