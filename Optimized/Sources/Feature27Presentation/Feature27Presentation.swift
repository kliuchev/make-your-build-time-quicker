import Feature27Domain
import Feature27Data

public enum Feature27PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature27DomainModel = Feature27DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
