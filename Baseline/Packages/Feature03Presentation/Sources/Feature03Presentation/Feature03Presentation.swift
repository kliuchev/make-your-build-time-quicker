import Feature03Domain
import Feature03Data

public enum Feature03PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature03DomainModel = Feature03DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
